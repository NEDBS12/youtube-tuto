package dev.course.receipt;

import java.util.Map;

import org.springframework.core.io.ClassPathResource;
import org.springframework.util.MimeType;
import org.springframework.util.MimeTypeUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ReceiptController {

    private final ReceiptService service;

    public ReceiptController(ReceiptService service) {
        this.service = service;
    }

    // upload your own photo: curl -F "file=@my-receipt.jpg" localhost:8080/receipts
    @PostMapping("/receipts")
    public Map<String, Object> upload(@RequestParam MultipartFile file) {
        return check(service.read(file.getResource(), MimeType.valueOf(file.getContentType())));
    }

    // the two samples in src/main/resources/receipts: cafe, hardware
    @GetMapping("/receipts/sample/{name}")
    public Map<String, Object> sample(@PathVariable String name) {
        return check(service.read(new ClassPathResource("receipts/" + name + ".png"), MimeTypeUtils.IMAGE_PNG));
    }

    @GetMapping("/describe/{name}")
    public String describe(@PathVariable String name) {
        return service.describe(new ClassPathResource("receipts/" + name + ".png"), MimeTypeUtils.IMAGE_PNG);
    }

    private Map<String, Object> check(Receipt r) {
        return Map.of("receipt", r, "addsUp", r.addsUp());
    }

}
