<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { module, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Toggle } from '$lib/button';
	import { Meta, Log } from '$lib/macro';
	import Button from './button.svelte';

	import { Status, Photo, Title, Date, Description, Content_, Tags, Author, Comment } from '.';
	import Engagament from './engage/engagement.svelte';
	import Like from './engage/like.svelte';
	import Share from './engage/share.svelte';
	import Highlight from './highlight.svelte';
	import Similar from './similar.svelte';
	import ToTop from './to_top.svelte';

	let { data } = $props();
	let item = $derived(data.item);
	let edit_mode = $state(false);
	let is_admin = $state(false);

	const update = (data) => {
		item = data;
	};

	let engagament = $state();
	let author = $state();
	let comment = $state();
	let similar = $state();

	const refresh = async (data) => {
		item = data;
		edit_mode = false;
		await engagament.load();
		await author.load();
		await comment.load();
		await similar.load();
	};

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access/post:edit`);
		resp = await resp.json();
		if (resp.status == 200) {
			is_admin = app.user.access.some((x) => resp.access.includes(x));
		}

		refresh(item);

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			window.history.replaceState(history.state, '', page.url.href);
		}
	});

	let edata = $state({
		comment: 0,
		like: 0,
		dislike: 0,
		share: 0,
		view: 0,
		user_like: null
	});
</script>

{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'post'} />
{/key}
<Meta title={item.title} description={item.description} image={item.photo} />

<Content>
	{#if is_admin}
		<Toggle state_2="edit" active={edit_mode} onclick={() => (edit_mode = !edit_mode)} />
		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('post:edit_status') || app.user.access.includes('post:edit_highlight'))}
		<div class="line status">
			<Status {item} {update}></Status>
			<Highlight {item} />
		</div>
	{/if}
	<Photo bind:item {edit_mode} {update} />
	<Title {item} {edit_mode} {update} />
	<Description {item} {edit_mode} {update} />
	<div class="line space date">
		<Date {item} {edit_mode} {update}></Date>
		<Engagament {item} bind:edata bind:this={engagament} />
	</div>
	<Content_ {item} {edit_mode} {update} />
	<Tags {item} {edit_mode} {update} />
	<Author {item} {edit_mode} bind:this={author} />
</Content>

<Content --content-background-color="var(--bg2)" --content-height>
	<div class="line engage">
		<Like {item} bind:edata />
		<Share {item} />
	</div>
	<Comment post={item} bind:this={comment} />
</Content>

<Content --content-height --content-padding-top="0" --content-padding-bottom="0">
	<Similar key={item.key} bind:this={similar} {refresh} />
	<ToTop />
</Content>

<style>
	.line.status {
		margin-bottom: 8px;
	}
	.line.date {
		align-items: flex-end;
	}
	.line.engage {
		gap: 16px;
	}
</style>
