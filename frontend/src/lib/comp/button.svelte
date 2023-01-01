<script>
	import SVG from './svg.svelte';

	export let href = '';

	export let name = '';
	export let tooltip = '';
	export let icon = '';
	export let icon_size = 20;
	export let color = '';
	export let active = false;
	let clas = '';
	export { clas as class };
	export let target = '';

	// let icon_only = !(name || $$slots);
	let icon_only = !name;
</script>

{#if href}
	<a
		class={clas}
		class:active
		class:icon_only
		style:color
		style:fill={color}
		{href}
		{target}
		title={tooltip}
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
		style:color
		style:fill={color}
		on:click|stopPropagation
		title={tooltip}
	>
		<SVG type={icon} size={icon_size} />
		{name}
		<slot />
	</button>
{/if}

<style>
	button,
	a {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--gap2);

		border: none;
		padding: var(--gap2);
		border-radius: var(--gap1);

		background-color: var(--mid_color);
		/* border: 2px solid var(--midtone); */
		/* border: 2px solid red; */
		/* background-color: transparent; */
		color: var(--light_color);
		fill: var(--light_color);

		text-decoration: none;
		font-weight: 500;

		width: fit-content;
	}

	/* .active,
	.primary {
		background-color: var(--color3);
		color: var(--light_color);
		fill: var(--light_color);
	} */

	/* .secondary {
		background-color: transparent;
		color: var(--midtone);
		border: 2px solid var(--background);
	} */

	/* .tertiary {
		padding: 0;
		border-radius: 0;
		color: var(--font);

		background-color: transparent;
		border-bottom: 2px solid var(--background);
	} */

	/* .link {
		padding: 0;
		color: var(--light_color);
		background-color: transparent;
	} */

	.tiny {
		gap: var(--gap1);
		padding: var(--gap1);
		font-size: small;
	}

	/* .tag {
		--size: 24px;
		height: var(--size);
		padding: 8px;

		border-radius: calc(var(--size) / 2);

		font-size: x-small;
		font-weight: unset;
	} */

	.wide {
		width: 100%;
	}

	/* .wide2 {
		width: 100%;
		max-width: 400px;
	} */

	/* .icon_only {
		--size: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		padding: 0;

		border-radius: var(--size);
	} */

	/* .icon_only.tiny {
		--size: 20px;

		width: var(--size);
		height: var(--size);
	} */

	:hover {
		background-color: var(--color1);
		/* color: var(--light_color); */
		/* fill: var(--light_color); */
	}

	:hover.hover.red {
		background-color: var(--color2);
	}

	/* .active:hover,
	.primary:hover {
		background-color: var();
	} */

	/* .tertiary:hover {
		background-color: transparent;
		border-color: var(--light_color);
		color: var(--light_color);
	} */

	/* .secondary:hover {
		background-color: transparent;
		color: var(--light_color);
		border: 2px solid var(--light_color);
	} */

	/* .link:hover {
		background-color: transparent;
		color: var();
	} */
</style>
