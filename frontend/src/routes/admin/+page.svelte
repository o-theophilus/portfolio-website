<script>
	import { module, _portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Manage_Video from './__manage_video__.svelte';

	export let data;
	let { setting } = data;

	$: if ($_portal) {
		if ($_portal.for == 'setting') {
			setting = $_portal.data;
		}

		$_portal = {};
	}
</script>

<Meta title="Admin Dashboard" description="This contains this website settingd" />

<Content>
	<br />
	<strong class="big">Website Settings</strong>
	<br /><br />
	<div class="hr" />
	<br />

	<strong> Featured Post{setting.featured_posts.length > 0 ? 's' : ''}: </strong>
	<br />
	{#each setting.featured_posts as post}
		{post}
		<br />
	{:else}
		No Featured Post
		<br />
	{/each}
	<br />
	<Button
		on:click={async () => {
			$module = {
				module: Manage_Video,
				setting
			};
		}}>Edit</Button
	>
	<br /><br />
</Content>

<style>
	.big {
		color: var(--accent1);
	}
</style>
