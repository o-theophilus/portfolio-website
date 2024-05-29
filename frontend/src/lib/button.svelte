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
		gap: var(--sp1);

		border: none;
		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: var(--ac3);
		color: var(--ac5_);
		fill: var(--ac5_);

		text-decoration: none;
		width: fit-content;

		cursor: pointer;
	}

	.tiny {
		/* gap: var(--sp1); */
		padding: var(--sp1);
		font-size: small;
	}
	.secondary {
		padding: 0;
		background-color: transparent;
		border-bottom: 2px solid transparent;
		color: var(--ac2);
		fill: var(--ac3);
		border-radius: 0;
	}

	.wide {
		width: 100%;
	}
	.careful {
		background-color: var(--cl2);
	}

	:hover {
		background-color: var(--cl1);
		text-decoration: none;
	}

	.secondary:hover {
		background-color: transparent;
		color: var(--cl1);
		fill: var(--cl1);
		border-bottom-color: var(--cl1);
	}

	:hover.red {
		background-color: var(--cl2);
	}
</style>
