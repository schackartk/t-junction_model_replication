# Article contents

The article is built using the [ReScience C article template](https://github.com/ReScience/template), with slight modifications.

# Creating the article PDF

The following command can be used to generate the article PDF document (`article.pdf`):

```sh
$ make
```

However, issues with `metadata.tex` can cause this to fail. Continue reading for likely solution.

### Remove `metadata.tex`

First remove `metadata.tex` and regenerate it from `metadata.yaml`.

```sh
$ rm metadata.tex
$ make metadata.tex
```

### Create `article.pdf`

```sh
$ make
```
