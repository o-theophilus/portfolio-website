<script>
	import { page } from '$app/stores';
	import { theme } from '$lib/store.js';
	import SVG from '$lib/comp/svg.svelte';

	$: is_home = $page.url.pathname == '/';
</script>

<button
	class:is_home
	on:click={() => {
		$theme = $theme == 'dark' ? 'light' : 'dark';
	}}
	on:keypress
>
	<div class="switch" class:dark={$theme == 'dark'}>
		<div class="state">
			<SVG type="light" size="15" />
		</div>
		<div class="state">
			<SVG type="dark" size="12" />
		</div>
	</div>
</button>

<style>
	button,
	.state {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	button {
		--size: 20px;

		position: relative;
		overflow: hidden;

		fill: var(--font);
		border-radius: 50%;

		height: var(--size);
		width: var(--size);

		margin: auto var(--gap2);
		background-color: transparent;
		border: none;

		transition-timing-function: ease-in-out;
	}

	.is_home {
		fill: var(--background);
	}

	button:hover {
		color: var(--light_color);
		background-color: var(--color1);
	}

	.switch {
		position: absolute;
		top: 0;

		transition: top var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.dark {
		top: -100%;
	}

	.state {
		width: var(--size);
		height: var(--size);
	}
</style>
