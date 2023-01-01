<script>
	import { page } from '$app/stores';

	export let link;
	$: path = $page.url.pathname.split('/')[1];
</script>

<a class:active={link == path} href="/{link}">
	<div class="highlight" />
	<div class="text">
		<slot />
	</div>
</a>

<style>
	a {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;

		padding: var(--gap2);

		text-decoration: none;
		color: var(--font);

		border-bottom: 2px solid transparent;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a:hover {
		color: var(--light_color);
	}

	a:hover .highlight {
		width: 100%;
		height: 100%;
		opacity: 1;

		border-radius: var(--gap1);
	}
	.active {
		font-weight: bold;
		border-color: var(--mid_color);
	}

	.text {
		position: relative;
	}

	.highlight {
		position: absolute;
		border-radius: 100%;

		width: 0%;
		height: 0%;
		background-color: var(--color1);
		opacity: 0;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
</style>
