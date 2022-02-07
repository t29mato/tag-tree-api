
``` mermaid
%%{init:{'theme':'neutral'}}%%
erDiagram
    node }|--|| tag : contain
    node }|--|| tag_tree : contain
    tag }o--o{ tag_synonyms: text
    node {
        tag_id id
        parent_id id
    }
    tag {
        name string
        comment string
    }
    tag_tree {
        name string
        key string
        node_id id
    }
    tag_synonyms {
        from_tag_id id
        to_tag_id id
    }
```
