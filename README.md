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
2. Make changes, create pull request to `dev` branch
3. Peer review and merge to `dev` branch
4. Checkout branch `dev` and update docs by sphinx

```
# in /Trisight
cd site_files
make html

# Unix
cp build\html\. ..\docs

# cmd (Windows)
copy build\html\. ..\docs
```

5. Check the website update

# Contributor

- Gaohua Zheng
- Zidiefeng
