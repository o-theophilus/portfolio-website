<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Button, Toggle } from '$lib/button';
	import { Meta, Icon, Log } from '$lib/macro';

	import Photo from './photo.svelte';
	import Title from './title.svelte';
	import Date from './date.svelte';
	import Description from './description.svelte';
	import Content_ from './content.svelte';
	import Engage from './engage.svelte';
	import Engagement from './engage.view.svelte';
	import Author from './author.svelte';
	import Tags from './tags.svelte';
	import Edit_Status from './status.svelte';
	import Highlight from './highlight.svelte';
	import Comment from './comment/index.svelte';
	import Similar from './similar.svelte';

	import Refresh from './refresh.svelte';
	import ToTop from './to_top.svelte';

	let { data } = $props();
	let post = $derived(data.post);
	let edit_mode = $state(false);
	let is_admin = $state(false);
	let ready = $state(false);

	let content = $state();
	const update = (data) => {
		post = data;
		content.refresh(post);
		engagement.refresh();
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access/post:edit`);
		resp = await resp.json();
		if (resp.status == 200) {
			is_admin = app.user.access.some((x) => resp.access.includes(x));
		}

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			window.history.replaceState(history.state, '', page.url.href);
		}

		ready = true;
	});

	let author = $state();
	let engagement = $state();
	let comment = $state();
	let similar = $state();
	const refresh = async () => {
		edit_mode = false;
		author.reset();
		engagement.reset();
		comment.reset();
		similar.reset();
		await author.refresh();
		await engagement.refresh();
		await comment.refresh();
		await similar.refresh();
	};
</script>

{#key post.key}
	<Log action={'viewed'} entity_key={post.key} entity_type={'post'} />
	<Meta title={post.title} description={post.description} image={post.photo} />

	{#if ready}
		<Refresh {refresh} />
	{/if}

	<Content>
		{#if is_admin}
			<div class="toggle">
				<Toggle
					state_2="edit"
					active={edit_mode}
					onclick={() => {
						edit_mode = !edit_mode;
					}}
				/>
			</div>
		{/if}

		{#if edit_mode && (app.user.access.includes('post:edit_status') || (app.user.access.includes('post:edit_highlight') && post.status == 'active'))}
			<hr />
			<div class="line">
				{#if app.user.access.includes('post:edit_status') && edit_mode}
					<Button size="small" onclick={() => module.open(Edit_Status, { post, update })}>
						<Icon icon="edit" size="1.4" />
						<span> Edit Status: <strong>{post.status}</strong> </span>
					</Button>
				{/if}
				{#if app.user.access.includes('post:edit_highlight') && edit_mode && post.status == 'active'}
					<Highlight post_key={post.key} />
				{/if}
			</div>
		{/if}

		<Photo {post} {edit_mode} {update} />
		<Title {post} {edit_mode} {update} />
		<Description {post} {edit_mode} {update} />
		<Date {post} {edit_mode} {update}>
			<Engagement post_key={post.key} bind:this={engagement} />
		</Date>
		<Content_ {post} {edit_mode} {update} bind:this={content} />
		<Tags {post} {edit_mode} {update} />
		<Author {post} {edit_mode} bind:this={author} />
		<Engage {post} {update} />
		<Comment {post} bind:this={comment} />
		<Similar post_key={post.key} bind:this={similar} />

		<ToTop />
	</Content>
{/key}

<style>
	hr {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
