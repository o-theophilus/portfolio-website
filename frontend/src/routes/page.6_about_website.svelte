<script>
	import Observe from '$lib/observe.svelte';
	import Content from '$lib/content.svelte';
</script>

<Content>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big">This Website</strong>
			<br /><br />
			This website was made with Svelte<span class="heart">&#10084</span> and deployed on Vercel.
			It's entirely static through the SvelteKit's SSG feature.
			<br /> <br />
			Posts are written in Markdown, in-page codes are formatted using Highlight.js and then converted
			to nice-looking HTML at build-time.
			<br /> <br />
			This website was originally built with C# and Razor then ported to React and now to SvelteKit because
			of its simplicity and ease of use.
			<br /><br />
			This website is an all-in-one blog, portfolio and pet project to try out new shiny things.
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
