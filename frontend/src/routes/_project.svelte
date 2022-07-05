<script>
	import { projects } from '$lib/db.js';

	import Content from '$lib/pageContent.svelte';
	import ItemBox from '$lib/itemBox.svelte';

	let items = projects;

	// let selected = [0, 3];
	// let len = 5 - selected.length;

	// for (let n = 0; n < len; n++) {
	// 	let num = Math.floor(Math.random() * projects.length);
	// 	while (selected.includes(num)) {
	// 		num = Math.floor(Math.random() * projects.length);
	// 	}
	// 	selected.push(num);
	// }

	// let items = [];

	// for (let n = 0; n < selected.length; n++) {
	// 	items.push(projects[selected[n]]);
	// }
</script>

<div class="proj">
	<div class="title">
		<div class="block">
			<h1>Projects</h1>
		</div>
	</div>

	<Content>
		{#each items as item}
			<ItemBox {item} />
		{:else}
			<p>No Project found</p>
		{/each}
	</Content>
</div>

<style>
	.proj {
		background-color: var(--color3);
		position: relative;
	}

	.title {
		height: var(--headerHeight);

		position: sticky;
		top: 0;
		z-index: 1;

		background-color: var(--color3);
		box-shadow: 0 5px 12px var(--color2);

		transition: top var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	.block {
		display: flex;
		align-items: center;

		max-width: var(--mobileWidth);
		margin: auto;

		padding: 0 var(--pad);
	}

	@media screen and (min-width: 900px) {
		.title {
			top: var(--headerHeight);
		}
	}

	h1 {
		color: var(--fColor1);
	}
</style>
