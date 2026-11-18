package dev.course.receipt;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.util.MimeType;

@Service
public class ReceiptService {

    private final ChatClient chatClient;

    public ReceiptService(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("""
                    You read photos of shop receipts and extract the data exactly as printed.
                    Copy names and numbers from the image. Never guess a value you can't read.""")
            .build();
    }

    public Receipt read(Resource image, MimeType type) {
        return chatClient.prompt()
            .user(u -> u.text("Extract the shop name, the date, every item line, the tax and the final total.")
                .media(type, image))
            .call()
            .entity(Receipt.class);
    }

    public String describe(Resource image, MimeType type) {
        return chatClient.prompt()
            .user(u -> u.text("Describe this image in two sentences.").media(type, image))
            .call()
            .content();
    }

}
