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
	let item = $derived(data.item);
	let edit_mode = $state(false);
	let is_admin = $state(false);

	const update = (data) => {
		item = data;
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

{#key item.key}
	<Log action={'viewed'} entity_key={item.key} entity_type={'post'} />
{/key}
<Meta title={item.title} description={item.description} image={item.photo} />

<Content>
	{#if is_admin}
		<Toggle state_2="edit" active={edit_mode} onclick={() => (edit_mode = !edit_mode)} />
		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('post:edit_status') || (app.user.access.includes('post:edit_highlight') && item.status == 'active'))}
		<hr />
		<div class="line">
			{#if app.user.access.includes('post:edit_status') && edit_mode}
				<Button
					onclick={() =>
						module.open(Status, {
							key: item.key,
							status: item.status,
							photo: item.photo,
							update
						})}
				>
					Edit Status: <span class="status {item.status}">{item.status}</span>
				</Button>
			{/if}
			{#if app.user.access.includes('post:edit_highlight') && edit_mode && item.status == 'active'}
				<Highlight {item} />
			{/if}
		</div>
		<br />
	{/if}

	<Photo bind:item {edit_mode} {update} />
	<Title {item} {edit_mode} {update} />
	<Description {item} {edit_mode} {update} />
	<Date {item} {edit_mode} {update}>
		<Engagement key={item.key} bind:this={engagement} />
	</Date>
	<Content_ {item} {edit_mode} {update} />
	<Tags {item} {edit_mode} {update} />
	<Author {item} {edit_mode} bind:this={author} />
	<Engage {item} {update} />
	<Comment post={item} bind:this={comment} />
	<Similar key={item.key} bind:this={similar} {refresh} />
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
