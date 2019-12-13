package com.biblograpycloud.publications.managers;

import com.biblograpycloud.publications.dao.PublicationRepo;
import com.biblograpycloud.publications.dao.entity.Publication;
import com.biblograpycloud.publications.dao.entity.UserFile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Service
public class PublicationManager {

    private PublicationRepo publicationRepo;

    @Autowired
    public PublicationManager(PublicationRepo publicationRepo) {
        this.publicationRepo = publicationRepo;
    }

    public Publication save(Publication publication) {
        return publicationRepo.save(publication);
    }

    public Iterable<Publication> getAll() {
        return publicationRepo.findAll();
    }

    public Optional<Publication> getById(long id) {
        return publicationRepo.findById(id);
    }

    public Iterable<Publication> getWithPagesBetween(int a, int b) {
        return publicationRepo.findAllByPageCountBetween(a, b);
    }


    @EventListener(ApplicationReadyEvent.class)
    public void createInitialRecords() {
        var file = new UserFile("jan", "test.pdf");
        List<UserFile> list = Arrays.asList(file);

        save(new Publication("Drugie prawo Kopernika", 220, 1526, list));
        save(new Publication("Pomiary - czlyli jak uwalić 50%", 170, 2000, new ArrayList<>()));
    }
}
