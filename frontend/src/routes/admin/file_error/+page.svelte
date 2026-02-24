<script>
	import { Button } from '$lib/button';
	import { Note, PageNote } from '$lib/info';
	import { Card, Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, loading, notify } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	let { data } = $props();
	let { users, posts } = data;
	let unused_user_photo = $state(data.unused_user_photo);
	let unused_post_photo = $state(data.unused_post_photo);

	let open_unused_user = $derived(unused_user_photo.length > 0);
	let open_unused_post = $derived(unused_post_photo.length > 0);
	let open_users = $state(users.length > 0);
	let open_posts = $state(posts.length > 0);

	let selected_user_photo = $state([]);
	let selected_post_photo = $state([]);
	let error = $state({});

	const remove = async (photos, entity) => {
		error = {};

		loading.open(`Deleting ${entity} photo . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/file_error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ photos, entity })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open(`${entity} photo${photos.length > 1 ? 's' : ''} deleted`);

			if (entity == 'user') {
				unused_user_photo = unused_user_photo.filter((x) => !photos.includes(x));
				selected_user_photo = [];
			} else if (entity == 'post') {
				unused_post_photo = unused_post_photo.filter((x) => !photos.includes(x));
				selected_post_photo = [];
			}
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Manage / Excess Files" />

<Content>
	<div class="page_title">Photo Error</div>

	<br />

	<Card
		open={open_unused_user}
		onclick={() => {
			open_unused_user = !open_unused_user;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{unused_user_photo.length} Unused User Photo{unused_user_photo.length > 1 ? 's' : ''}
			</div>
		{/snippet}

		{#if unused_user_photo.length}
			<div class="photo_area">
				{#each unused_user_photo as x (x)}
					<img
						animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
						class:selected={selected_user_photo.includes(x)}
						src={x.slice(-4) == '.jpg' ? `${x}/100` : '/no_preview.png'}
						loading="lazy"
						alt="unused file"
						onclick={() => {
							if (selected_user_photo.includes(x)) {
								selected_user_photo = selected_user_photo.filter((y) => y != x);
							} else {
								selected_user_photo.push(x);
								selected_user_photo = selected_user_photo;
							}
						}}
						onerror={(e) => (e.target.src = '/no_photo.png')}
						role="presentation"
					/>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No photo here</div>
			</PageNote>
		{/if}

		<Note status="400" note={error.user} --note-margin-top="16px"></Note>

		{#if unused_user_photo.length > 0}
			<div class="line btns">
				<Button
					onclick={() => {
						if (selected_user_photo.length != unused_user_photo.length) {
							selected_user_photo = [...unused_user_photo];
						} else {
							selected_user_photo = [];
						}
					}}
				>
					Select
					{#if selected_user_photo.length != unused_user_photo.length}
						All
					{:else}
						None
					{/if}
				</Button>
				<Button
					extra="hover_red"
					onclick={() => {
						remove(selected_user_photo, 'user');
					}}
					disabled={selected_user_photo.length == 0}
				>
					Delete ({selected_user_photo.length})
				</Button>
			</div>
		{/if}
	</Card>

	<Card
		open={open_unused_post}
		onclick={() => {
			open_unused_post = !open_unused_post;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{unused_post_photo.length} Unused post Photo{unused_post_photo.length > 1 ? 's' : ''}
			</div>
		{/snippet}

		{#if unused_post_photo.length}
			<div class="photo_area">
				{#each unused_post_photo as x (x)}
					<img
						animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
						class:selected={selected_post_photo.includes(x)}
						src={x.slice(-4) == '.jpg' ? `${x}/100` : '/no_preview.png'}
						loading="lazy"
						alt="unused file"
						onclick={() => {
							if (selected_post_photo.includes(x)) {
								selected_post_photo = selected_post_photo.filter((y) => y != x);
							} else {
								selected_post_photo.push(x);
								selected_post_photo = selected_post_photo;
							}
						}}
						onerror={(e) => (e.target.src = '/no_photo.png')}
						role="presentation"
					/>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No photo here</div>
			</PageNote>
		{/if}

		<Note status="400" note={error.post} --note-margin-top="16px"></Note>

		{#if unused_post_photo.length > 0}
			<div class="line btns">
				<Button
					onclick={() => {
						if (selected_post_photo.length != unused_post_photo.length) {
							selected_post_photo = [...unused_post_photo];
						} else {
							selected_post_photo = [];
						}
					}}
				>
					Select
					{#if selected_post_photo.length != unused_post_photo.length}
						All
					{:else}
						None
					{/if}
				</Button>
				<Button
					extra="hover_red"
					onclick={() => {
						remove(selected_post_photo, 'post');
					}}
					disabled={selected_post_photo.length == 0}
				>
					Delete ({selected_post_photo.length})
				</Button>
			</div>
		{/if}
	</Card>

	<Card
		open={open_users}
		onclick={() => {
			open_users = !open_users;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{users.length} user{users.length > 1 ? 's' : ''} with missing photo
			</div>
		{/snippet}

		{#if users.length}
			<div class="link_area">
				{#each users as x}
					<a class="link" href="/@{x.username}">{x.name}</a>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No user here</div>
			</PageNote>
		{/if}
	</Card>

	<Card
		open={open_posts}
		onclick={() => {
			open_posts = !open_posts;
		}}
	>
		{#snippet title()}
			<div class="group_title">
				{posts.length} post{posts.length > 1 ? 's' : ''} with missing photo
			</div>
		{/snippet}

		{#if posts.length}
			<div class="link_area">
				{#each posts as x}
					<a class="link" href="/{x.slug}">{x.name}</a>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="search" size="50" />
				<div class="none">No post here</div>
			</PageNote>
		{/if}
	</Card>
</Content>

<style>
	.group_title {
		font-weight: 800;
	}

	.photo_area {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	img {
		width: 100px;
		border-radius: 8px;
		cursor: pointer;
		background-color: var(--bg2);

		&.selected {
			outline: 2px solid var(--cl1);
		}
	}

	.btns {
		margin-top: 16px;
	}

	.link_area {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
		gap: 4px;

		& .link {
			display: flex;
			align-items: center;

			padding: 4px;
			border-radius: 4px;

			line-height: 120%;
			color: var(--ft2);
			font-size: 0.7rem;
			text-decoration: none;
			background-color: var(--bg3);
			outline: 1px solid var(--ol);
			outline-offset: -1px;

			transition: background-color 0.2s ease-in-out;
			&:hover {
				background-color: var(--bg2);
				color: var(--ft1);
			}
		}
	}

	.none {
		font-size: 0.8rem;
	}
</style>
