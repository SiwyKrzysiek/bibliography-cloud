package com.biblograpycloud.publications.dao.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
public class Publication {

    public Publication(String title, Integer pageCount, Integer publicationYear, List<UserFile> attachments) {
        this.title = title;
        this.pageCount = pageCount;
        this.publicationYear = publicationYear;
        this.attachments = attachments;
    }

    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    private Long id;

    private String title;

    private Integer pageCount;

    private Integer publicationYear;

    @OneToMany(targetEntity = UserFile.class, cascade = CascadeType.ALL)
    @JoinColumn(name = "publication_fk", referencedColumnName = "id")
    private List<UserFile> attachments;
}
