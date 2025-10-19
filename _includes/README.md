# Includes 文件夹说明

这个文件夹包含可复用的 Jekyll 代码片段，用于在主页面中显示不同类型的项目列表。

## 文件说明

### 1. `research_list.html`
- **用途**: 显示学术研究论文
- **数据源**: `_posts` 文件夹中 `categories: research` 的文章
- **显示字段**: 
  - 标题、作者、会议/期刊、年份
  - 链接: arxiv, video, code, poster, slides, website, youtube

### 2. `projects_list.html`
- **用途**: 显示个人项目
- **数据源**: `_projects` 文件夹中的所有文件
- **显示字段**: 
  - 标题
  - 链接: code, website, paper

### 3. `other_projects_list.html`
- **用途**: 显示其他类型的项目（课程作业、side projects 等）
- **数据源**: `_posts` 文件夹中非 `research` 和非 `Intel` 类别的文章
- **显示字段**: 
  - 标题、类别、课程、日期
  - 链接: website, paper, patent, video, code, poster, slides

## 如何使用

在 `_layouts/default.html` 中通过 `{% include %}` 语句引用：

```liquid
{% include research_list.html %}
{% include projects_list.html %}
{% include other_projects_list.html %}
```

## 如何修改

如果你想修改某个部分的显示逻辑：
1. 打开对应的 `.html` 文件
2. 修改 HTML 结构或 Liquid 逻辑
3. 保存后刷新网站即可看到效果

## 优点

- ✅ 代码模块化，易于维护
- ✅ 每个部分的逻辑独立，互不干扰
- ✅ 修改某个部分不会影响其他部分
- ✅ 代码更清晰，易于理解

