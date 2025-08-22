<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Toggle } from '$lib/button';
	import { Meta, Log } from '$lib/macro';
	import Button from './button.svelte';

	import {
		Status,
		Photo,
		Title,
		Date,
		Description,
		Content_,
		Tags,
		Author,
		Engage,
		Comment
	} from '.';
	import Engagement from './engagement.svelte';
	import Highlight from './highlight.svelte';
	import Similar from './similar.svelte';
	import ToTop from './to_top.svelte';

	let { data } = $props();
	let post = $derived(data.post);
	let edit_mode = $state(false);
	let is_admin = $state(false);

	const update = (data) => {
		post = data;
	};

	let author = $state();
	let engagement = $state();
	let comment = $state();
	let similar = $state();

	const refresh = async () => {
		edit_mode = false;
		await author.load();
		await engagement.load();
		await comment.load();
		await similar.load();
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access/post:edit`);
		resp = await resp.json();
		if (resp.status == 200) {
			is_admin = app.user.access.some((x) => resp.access.includes(x));
		}

		refresh();

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			window.history.replaceState(history.state, '', page.url.href);
		}
	});
</script>

{#key post.key}
	<Log action={'viewed'} entity_key={post.key} entity_type={'post'} />
{/key}
<Meta title={post.title} description={post.description} image={post.photo} />

<Content>
	{#if is_admin}
		<Toggle state_2="edit" active={edit_mode} onclick={() => (edit_mode = !edit_mode)} />
		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('post:edit_status') || (app.user.access.includes('post:edit_highlight') && post.status == 'active'))}
		<hr />
		<div class="line">
			{#if app.user.access.includes('post:edit_status') && edit_mode}
				<Button
					onclick={() =>
						module.open(Status, {
							key: post.key,
							status: post.status,
							photo: post.photo,
							update
						})}
				>
					Edit Status: <span class="status {post.status}">{post.status}</span>
				</Button>
			{/if}
			{#if app.user.access.includes('post:edit_highlight') && edit_mode && post.status == 'active'}
				<Highlight {post} />
			{/if}
		</div>
		<br />
	{/if}

	<Photo bind:post {edit_mode} {update} />
	<Title {post} {edit_mode} {update} />
	<Description {post} {edit_mode} {update} />
	<Date {post} {edit_mode} {update}>
		<Engagement post_key={post.key} bind:this={engagement} />
	</Date>
	<Content_ {post} {edit_mode} {update} />
	<Tags {post} {edit_mode} {update} />
	<Author {post} {edit_mode} bind:this={author} />
	<Engage {post} {update} />
	<Comment {post} bind:this={comment} />
	<Similar post_key={post.key} bind:this={similar} {refresh} />
	<ToTop />
</Content>

<style>
	hr {
		margin-bottom: var(--sp2);
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
	.status {
		font-weight: 800;
	}

	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}
</style>
