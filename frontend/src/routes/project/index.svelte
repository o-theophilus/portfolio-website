<script context="module">
	export const prerender = true;
</script>

<script>
	import { projects } from '$lib/db.js';

	import Image from '$lib/pageImage.svelte';
	import Content from '$lib/pageContent.svelte';
	import ItemBox from '$lib/itemBox.svelte';
	import Meta from '$lib/meta.svelte';
</script>

<Meta title="Projects - Theophilus" description="Stuff I Made." image="/images/akropol_001.jpg" />

<Image src="project" copy="Projects" text="Stuff I Made" />

<Content>
	{#each projects as item}
		<ItemBox {item} />
	{:else}
		<p>No Project found</p>
	{/each}
</Content>
