<script>
	import { notify } from '$lib/store.svelte.js';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import Item from './notify.item.svelte';
</script>

<section>
	{#each notify.value as item (item.key)}
		<div
			class="one"
			transition:fade={{ delay: 0, duration: 250, easing: cubicInOut }}
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
		>
			<Item {item} />
		</div>
	{/each}
</section>

<style>
	section {
		z-index: 1;
		
		position: fixed;
		top: var(--headerHeight);
		right: 0;

		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: var(--sp1);

		pointer-events: none;
	}
</style>
