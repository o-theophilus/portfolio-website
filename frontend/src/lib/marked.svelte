<script>
	import marked from 'marked';
	import hljs from 'highlight.js';
	import '$lib/style/marked.css';

	marked.setOptions({
		renderer: new marked.Renderer(),
		highlight: function (code, lang) {
			const language = hljs.getLanguage(lang) ? lang : 'plaintext';
			return hljs.highlight(code, { language }).value;
		}
		// pedantic: false,
		// gfm: true,
		// breaks: false,
		// sanitize: false,
		// smartLists: true,
		// smartypants: false,
		// xhtml: false
	});

	export let md = `	
---
# HEADERS

# This is an \\<h1> tag
## This is an \\<h2> tag
###### This is an \\<h6> tag

	
---
# EMPHASIS

*This text will be italic*

**This text will be bold**

*You **can** combine them*


---
# BLOCKQUOTES

> I’ve always been more interested
> in the future than in the past.


---
# LISTS

* Item 1
* Item 2
   * Item 2a
   * Item 2b

1. Item 1
1. Item 2
1. Item 3
   * Item 3a
   * Item 3b


---
# IMAGES

![GitHub Logo](/images/akropol_001.jpg)


---
# LINKS

http://github.com - automatic!

or

[GitHub](http://github.com)


---
# BACKSLASH ESCAPES

\\*literal asterisks*


---
# FENCED CODE BLOCKS

\`\`\`javascript
function test() {
	console.log("look ma’, no spaces");
\`\`\`


---
# TASK L ISTS

1. [x] done
* [ ] undone

	
---
# TABLES

First Header | Second Header
------------ | -------------
Content cell 1 | Content cell 2
Content column 1 | Content column 2

	`;
</script>

{@html marked(md)}
