<script>
	import Observe from '$lib/observe.svelte';
	import Content from '$lib/content.svelte';
</script>

<Content>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big">This Website</strong>
			<br /><br />

			I built this website using Svelte<span class="heart">&#10084</span> and SvelteKit, two
			cutting-edge technologies that make it easy to create fast, responsive web applications.
			Unlike traditional static sites, this website is dynamic and interactive, which means it can
			be updated in real-time without needing to refresh the page.
			<br /> <br />
			Posts are written in Markdown, a lightweight markup language that's easy to learn and use. Markdown
			simplifies the process of formatting text, so you can focus on creating great content without worrying
			about complex HTML syntax. Thanks to the integration of Highlight.js, the code snippets on this
			website are beautifully highlighted, making it easy for you to follow along and understand the
			technical details.
			<br /><br />
			Whether you're reading my post, or just exploring, I hope you'll enjoy your
			experience on this site. This website is an all-in-one platform where I showcase my work and try
			out new shiny things.
		</div>
	</Observe>
</Content>

<style>
	.heart {
		color: var(--color2);
	}
	.observe {
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: all 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}
	.big {
		color: var(--accent1);
	}
</style>
