<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	import { Switch } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';

	import { Author, Comment, Content_, Date, Description, Photo, Status, Tags, Title } from '.';
	import Engagement from './engage/engagement.svelte';
	import Like from './engage/like.svelte';
	import Share from './engage/share.svelte';
	import Highlight from './highlight.svelte';
	import Similar from './similar.svelte';
	import ToTop from './to_top.svelte';

	let { data } = $props();
	let post = $derived(data.post);
	let edit_mode = $state(false);
	let is_admin = app.user.access.some((x) =>
		[
			'post:add',
			'post:edit_photo',
			'post:edit_title',
			'post:edit_date',
			'post:edit_description',
			'post:edit_content',
			'post:edit_files',
			'post:edit_tags',
			'post:edit_status',
			'post:edit_author',
			'post:edit_highlight'
		].includes(x)
	);

	let loading = $state(false);
	let engagement = $state({});
	let author = $state({});
	let comment_resp = $state([]);
	let similar = $state([]);

	const update = async (data) => {
		post = data;
		edit_mode = false;
		loading = true;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/after/${post.key}`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});

		resp = await resp.json();
		loading = false;

		if (resp.status == 200) {
			engagement = resp.engagement;
			author = resp.author;
			comment_resp = resp.comment_resp;
			similar = resp.similar;
		}
	};

	onMount(async () => {
		update(post);

		if (page.url.searchParams.has('edit') && is_admin) {
			page.url.searchParams.delete('edit');
			edit_mode = true;
			replaceState(page.url.href);
		}
	});
</script>

{#key post.key}
	<Log action={'viewed'} entity_key={post.key} entity_type={'post'} />
{/key}
<Meta title={post.title} description={post.description} image={post.photo} />

<Content --content-background-color="var(--bg)">
	{#if is_admin}
		<Switch
			--toggle-height="21px"
			--toggle-font-size="0.8rem"
			--toggle-padding-x="8px"
			list={['', 'edit']}
			value={!edit_mode ? '' : 'edit'}
			onclick={() => {
				edit_mode = !edit_mode;
			}}
		/>

		<br />
	{/if}

	{#if edit_mode && (app.user.access.includes('post:edit_status') || app.user.access.includes('post:edit_highlight'))}
		<div class="line status">
			<Status item={post} {update}></Status>
			<Highlight item={post} />
		</div>
	{/if}
	<Photo bind:item={post} {edit_mode} {update} />
	<Title item={post} {edit_mode} {update} />
	<Description item={post} {edit_mode} {update} />
	<div class="line space date">
		<Date item={post} {edit_mode} {update}></Date>
		<Engagement {engagement} {loading} />
	</div>
	<Content_ item={post} {edit_mode} {update} />
	<Tags item={post} {edit_mode} {update} />
	<Author {author} {post} {edit_mode} {loading} {update} />
</Content>

<Content --content-height>
	<div class="line engage">
		<Like {post} bind:engagement />
		<Share item={post} />
	</div>

	<hr />

	<Comment {post} {comment_resp} {loading} />
</Content>

<Content
	--content-background-color="var(--bg2)"
	--content-height="auto"
	--content-padding-top="1px"
	--content-padding-bottom="1px"
>
	<Similar {similar} {loading} {update} />
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
