<script>
	import markdownIt from 'markdown-it';
	import highlightjs from 'markdown-it-highlightjs';
	import video from 'markdown-it-video';
	import './marked.css';

	const md = markdownIt({
		html: true,
		linkify: true,
		typographer: true
	})
		.use(highlightjs)
		.use(video, {
			youtube: { width: '100%', height: 500 }
		});

	// https://markdown-it.github.io/

	export let content = '';
</script>

<section class="markdown">
	{@html md.render(content)}
</section>
