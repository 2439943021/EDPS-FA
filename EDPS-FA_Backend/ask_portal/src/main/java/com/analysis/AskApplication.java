package com.analysis;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @author ChenJG
 * @date 2024/3/11 23:59
 */
@SpringBootApplication(scanBasePackages = {"com.analysis.**"})
//@EnableScheduling
public class AskApplication {
    public static void main(String[] args) {
        SpringApplication.run(AskApplication.class, args);
    }
}
