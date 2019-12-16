package com.biblograpycloud.publications.api;

import com.biblograpycloud.publications.dao.entity.Publication;
import com.biblograpycloud.publications.dto.Translator;
import com.biblograpycloud.publications.dto.errors.PublicationAlreadyExistsMessage;
import com.biblograpycloud.publications.managers.PublicationManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

@RestController
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class PublicationApi {

    private PublicationManager publicationManager;

    @Autowired
    public PublicationApi(PublicationManager publicationManager) {
        this.publicationManager = publicationManager;
    }

    @GetMapping("/users/{user}/publications/all")
    public ResponseEntity<?> getAllUserPublication(@PathVariable String user) {
        // TODO: Cleanup link tests
//        var link = new Link("/place", "next");
        var link = linkTo(methodOn(PublicationApi.class).getAllUserPublication(user)).withRel("me");
        System.out.println(link);

//        Link selfLink = link.andAffordance(afford(methodOn(PublicationApi.class).deletePublication(user, 1)));

        var publications = publicationManager.getAllUserPublications(user);
        var mapped = StreamSupport.stream(publications.spliterator(), false)
                .map(p -> Translator.createPublicationDTOWithHATEOAS(p, user))
                .collect(Collectors.toList());


        return ResponseEntity.ok(mapped);
    }

    @GetMapping("/users/{user}/publications/{id}")
    public ResponseEntity<?> getOnePublication(@PathVariable String user, @PathVariable long id) {
        var publication = publicationManager.getById(id);

        if (publication.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new PublicationAlreadyExistsMessage());
        }

        var result = Translator.createPublicationDTOWithHATEOAS(publication.get(), user);
        return ResponseEntity.ok(result);
    }

    @DeleteMapping("/users/{user}/publications/{id}")
    public ResponseEntity<?> deletePublication(@PathVariable String user, @PathVariable long id) {
        // TODO: Make deleting work
        return ResponseEntity.ok(String.format("Publication number %d deleted", id));
    }

    @PostMapping
    public ResponseEntity addPublication(@RequestBody Publication publication) {
        var result = publicationManager.save(publication);

        return ResponseEntity.ok(result);
    }
}
