<script>
	import markdownIt from 'markdown-it';
	import highlightjs from 'markdown-it-highlightjs';
	import video from 'markdown-it-video';
	import linkAttributes from 'markdown-it-link-attributes';
	import './marked.css';

	const md = markdownIt({
		html: true,
		linkify: true,
		typographer: true
	})
		.use(highlightjs)
		.use(video, {
			youtube: { width: '100%', height: 500 }
		})
		.use(linkAttributes, {
			pattern: /^https?:\/\//,
			attrs: {
				target: '_blank'
			}
		});

	// https://markdown-it.github.io/

	let { content = '' } = $props();
</script>

<section class="markdown">
	{@html md.render(content)}
</section>
