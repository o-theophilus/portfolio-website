<script>
	import SVG from '$lib/svg.svelte';
	import { scroll } from '$lib/store.js';

	export let src = '';

	export let copy = '';
	export let text = '';
</script>

<section>
	<img src="/site/{src}.jpg" alt={src} />
	<div class="msg">
		<h1>{copy}</h1>
		<p>{text}</p>
	</div>
	<div
		class="scroll"
		on:click|stopPropagation={() => {
			scroll('.pageContent');
		}}
	>
		<SVG type="down" size="50" />
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		position: relative;
		width: 100vw;
		height: 100vh;

		padding: var(--headerHeight);
	}

	img {
		position: absolute;
		height: 100vh;

		object-fit: cover;
		z-index: -1;
	}
	.msg {
		max-width: var(--mobileWidth);

		font-size: 2em;
		text-align: center;
		color: white;

		text-shadow: 0 0 5px var(--color2);
	}
	.scroll {
		display: flex;
		justify-content: center;
		align-items: center;

		position: absolute;
		bottom: var(--headerHeight);
		--size: 100px;

		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		background-color: var(--colorNill);
		justify-self: flex-start;

		/* backdrop-filter: blur(2px); */
		fill: var(--color3);

		cursor: pointer;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.scroll:hover {
		background-color: var(--color4);
	}
</style>
