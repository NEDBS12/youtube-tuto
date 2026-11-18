package dev.course.docs;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.document.Document;
import org.springframework.ai.model.transformer.KeywordMetadataEnricher;
import org.springframework.ai.reader.markdown.MarkdownDocumentReader;
import org.springframework.ai.reader.markdown.config.MarkdownDocumentReaderConfig;
import org.springframework.ai.reader.pdf.PagePdfDocumentReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

@Service
public class IngestService {

    private static final Logger log = LoggerFactory.getLogger(IngestService.class);

    private static final PromptTemplate KEYWORDS = new PromptTemplate("""
            {context_str}

            Give 3 keywords for this text. Reply with the keywords only, comma separated.""");

    @Value("classpath:docs/employee-handbook.pdf")
    private Resource handbook;

    @Value("classpath:docs/it-help.md")
    private Resource itHelp;

    private final VectorStore vectorStore;
    private final ChatModel chatModel;

    public IngestService(VectorStore vectorStore, ChatModel chatModel) {
        this.vectorStore = vectorStore;
        this.chatModel = chatModel;
    }

    public IngestReport ingest() {
        // 1. Extract: one document per PDF page, one per Markdown section
        List<Document> pages = new PagePdfDocumentReader(handbook).get();
        List<Document> sections = new MarkdownDocumentReader(itHelp, MarkdownDocumentReaderConfig.builder()
                .withAdditionalMetadata("file_name", "it-help.md")
                .build()).get();
        log.info("EXTRACT {} PDF pages, {} Markdown sections", pages.size(), sections.size());

        // 2. Transform: clean the PDF text, split into small chunks, then add keywords
        List<Document> documents = new ArrayList<>(pages.stream().map(IngestService::clean).toList());
        documents.addAll(sections);
        List<Document> chunks = TokenTextSplitter.builder()
                .withChunkSize(100)
                .build()
                .apply(documents);
        chunks = KeywordMetadataEnricher.builder(chatModel)
                .keywordsTemplate(KEYWORDS)
                .build()
                .apply(chunks);
        log.info("TRANSFORM {} chunks, first one: {}", chunks.size(), chunks.get(0).getMetadata());

        // 3. Load: replace the old version of these files, then store
        vectorStore.delete("file_name in ['employee-handbook.pdf', 'it-help.md']");
        vectorStore.add(chunks);
        log.info("LOAD {} chunks into the vector store", chunks.size());
        return new IngestReport(pages.size(), sections.size(), chunks.size());
    }

    // PDF text keeps the page layout: "get 27  vacation  days"
    private static Document clean(Document page) {
        return page.mutate().text(page.getText().replaceAll("\\s+", " ").trim()).build();
    }
}
