<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { module, portal, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Fold from '$lib/button/fold.svelte';
	import Link from '$lib/button/link.svelte';
	import Login from '../../auth/login.svelte';
	import Icon from '$lib/icon.svelte';
	import Comment from './comment.svelte';
	import Add from './_add.svelte';
	import Sort from './sort.svelte';

	export let post;
	let comments = [];
	let open = true;

	$: if ($portal) {
		if ($portal.for == 'comment') {
			comments = $portal.data;
		}

		if (['comment'].includes($portal.for)) {
			$portal = {};
		}
	}

	let loading = true;
	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${post.key}`);
		resp = await resp.json();

		if (resp.status == 200) {
			comments = resp.comments;
		}

		loading = false;
	});
</script>

<div class="title">
	<strong class="ititle">
		{#if comments.length > 0}
			{comments.length}
		{/if}
		Comment{#if comments.length > 1}s{/if}
	</strong>

	{#if comments.length > 2}
		<!-- <Sort {post.key} /> -->
	{/if}

	<Fold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</div>

{#if open}
	<div class="comments" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#each comments as x}
			{#if x.path.length == 0}
				<Comment comment={x} {comments} post_key={post.key} />
			{/if}
		{:else}
			No comment
		{/each}
	</div>
{/if}

{#if $user.login}
	<Button
		on:click={() => {
			$module = {
				module: Add,
				post_key: post.key,
				path: []
			};
		}}
	>
		<Icon icon="add_comment" />
		Add comment
	</Button>
{:else}
	<Link
		on:click={() => {
			$module = {
				module: Login
			};
		}}
	>
		Login
	</Link> to add comment
{/if}

<br />

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;

		font-weight: 800;
		color: var(--ft1);
	}
	.comments {
		margin: var(--sp2) 0;
	}
</style>
