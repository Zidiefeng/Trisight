# Trisight

[Website](https://zidiefeng.github.io/Trisight/)

Trisight is a tool for stock analysis


## Install tools

```
pip install git+https://github.com/Zidiefeng/Trisight@dev
```

# How to contribute

## How to contribute

1. Create a new branch off from `dev` branch
2. Make and push changes, create pull request to `dev` branch
3. Peer review and merge to `dev` branch
4. Checkout branch `dev` and update docs by sphinx
5. Change config file if added new module: `site_files\source\index.rst`
6. Update html website:

```
pip install sphinx
cd Trisight/site_files
make html
```

7. Update docs for github page

    - If Unix:
    ```
    cp build\html\. ..\docs
    ```

    - If cmd (Windows):
    ```
    copy build\html\. ..\docs
    ```

5. Check the website update

# Contributor

# Data scientist: Gaohua Zheng
- Zidiefeng
