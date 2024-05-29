<script>
	import { module, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Manage_Video from './__manage_video__.svelte';

	export let data;
	console.log(data);
	let { posts } = data;

	$: if ($portal) {
		if ($portal.for == 'post') {
			posts = $portal.data;
		}

		$portal = {};
	}
</script>

<Meta title="Admin Dashboard" description="This contains this website settings" />

<Content>
	<strong class="big">Featured Posts</strong>
	<br /><br />
	<div class="hr" />
	<br />

	<strong> Featured Posts </strong>
	<br />
	{#each posts as x, i}
		{i + 1}. {x}
		<br />
	{:else}
		No Featured Post
	{/each}
	<br />
	<Button
		on:click={async () => {
			$module = {
				module: Manage_Video
				// setting
			};
		}}>Edit</Button
	>
	<br /><br />
</Content>

<style>
	.big {
		color: var(--ac1);
	}
</style>
