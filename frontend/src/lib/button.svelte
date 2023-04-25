<script>
	import SVG from './svg.svelte';

	let clas = '';
	export { clas as class };
	export let name = '';
	export let tooltip = '';
	export let href = '';
	export let target = '';

	export let icon = '';
	export let icon_size = 20;

	export let icon_color = '';

	let icon_only = name == '' && Object.keys($$slots).length == 0;
	export let active = false;
</script>

{#if href}
	<a
		class={clas}
		class:active
		class:icon_only
		style:fill={icon_color}
		title={tooltip}
		{href}
		{target}
	>
		<SVG type={icon} size={icon_size} />
		{name}
		<slot />
	</a>
{:else}
	<button
		class={clas}
		class:active
		class:icon_only
		style:fill={icon_color}
		title={tooltip}
		on:click|stopPropagation
	>
		<SVG type={icon} size={icon_size} />
		{name}
		<slot />
	</button>
{/if}

<style>
	button,
	a {
		display: inline-flex;
		justify-content: center;
		align-items: center;
		gap: var(--gap1);

		border: none;
		padding: var(--gap2);
		border-radius: var(--gap0);

		background-color: var(--accent3);
		color: var(--accent5_);
		fill: var(--accent5_);

		text-decoration: none;
		width: fit-content;

		cursor: pointer;
	}

	.tiny {
		/* gap: var(--gap1); */
		padding: var(--gap1);
		font-size: small;
	}
	.secondary {
		padding: 0;
		background-color: transparent;
		border-bottom: 2px solid transparent;
		color: var(--accent2);
		fill: var(--accent3);
		border-radius: 0;
	}

	.wide {
		width: 100%;
	}

	:hover {
		background-color: var(--color1);
		text-decoration: none;
	}

	.secondary:hover {
		background-color: transparent;
		color: var(--color1);
		fill: var(--color1);
		border-bottom-color: var(--color1);
	}

	/* .icon_only { */
		/* padding: 0; */
		/* fill: var(--accent5); */
		/* background-color: transparent; */
	/* } */

	/* .icon_only:hover { */
		/* fill: var(--color1); */
	/* } */

	:hover.hover.red {
		background-color: var(--color2);
	}
</style>
