package com.biblograpycloud.api.jwt;

import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import lombok.NonNull;
import org.springframework.beans.factory.annotation.Value;

import javax.crypto.spec.SecretKeySpec;
import java.security.Key;

/**
 * Class for validation JWT tokens
 */
public class JWTValidator {
    @Value("${jwt.secret}")
    private static String JWT_SECRET;

    public static boolean isFileListingTokenValid(@NonNull String token,@NonNull String userName) {
        try {
            System.out.println(JWT_SECRET);
            System.out.println(JWT_SECRET.getBytes().length);
            Key key = new SecretKeySpec(JWT_SECRET.getBytes(), "HmacSHA256");
            var reuslt = Jwts.parser().setSigningKey(key).parseClaimsJws(token);
            System.out.println("Dobry token");
            //OK, we can trust this JWT

        } catch (JwtException e) {
            return false;
            System.out.println("Zły token");
            //don't trust the JWT!
        }
    }
}
