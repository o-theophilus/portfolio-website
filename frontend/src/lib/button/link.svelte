<script>
	import SVG from '$lib/svg.svelte';

	export let href = '';
	export let target = '';
	export let disabled = false;

	export let icon = false;
</script>

{#if href}
	<a {href} {target}>
		<slot />

		{#if icon}
			<div class="svg">
				<SVG icon="angle" size="8" />
			</div>
		{/if}
	</a>
{:else}
	<button on:click {disabled}>
		<slot />

		{#if icon}
			<div class="svg">
				<SVG icon="angle" size="8" />
			</div>
		{/if}
	</button>
{/if}

<style>
	button,
	a {
		display: inline-flex;
		gap: var(--sp1);

		color: var(--cl1);
		font-weight: 700;
		text-decoration: none;
		border: none;
		background: none;
		cursor: pointer;

		fill: currentColor;
	}

	:hover {
		color: var(--cl1_b);
	}

	.svg {
		transform: scaleX(-1);
	}
</style>
