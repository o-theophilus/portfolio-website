<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import { loading, notify, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { FoldButton, Button, BackButton } from '$lib/button';
	import { Meta, Log, Icon } from '$lib/macro';
	import { PageNote, Note } from '$lib/info';

	let { data } = $props();
	let unused = $state(data.unused);
	let { users } = data;
	let { posts } = data;

	let open_unused = $derived(unused.length > 0);
	let open_users = $state(users.length > 0);
	let open_posts = $state(posts.length > 0);

	let files = $state([]);
	let error = $state({});

	const remove = async () => {
		error = {};

		loading.open('deleting . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/file_error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ files })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			unused = unused.filter((x) => !files.includes(x));
			notify.open(`Photo${files.length > 1 ? 's' : ''} Deleted`);
			files = [];
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Manage Files" description="Here you will find missing or excess images" />

<Content>
	<div class="line">
		<BackButton />
		<div class="page_title">Photo Error</div>
	</div>

	<div class="fold">
		<div class="group_title">
			Unused Photo{unused.length > 1 ? 's' : ''} / File{unused.length > 1 ? 's' : ''} ({unused.length})
			<FoldButton
				open={open_unused}
				onclick={() => {
					open_unused = !open_unused;
				}}
			/>
		</div>

		{#if open_unused}
			<div transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#if unused.length > 0}
					<div class="unused">
						{#each unused as x (x)}
							<img
								animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
								class:selected={files.includes(x)}
								src={x.slice(-4) == '.jpg' ? `${x}/100` : '/no_preview.png'}
								loading="lazy"
								alt="unused file"
								onclick={() => {
									if (files.includes(x)) {
										files = files.filter((y) => y != x);
									} else {
										files.push(x);
										files = files;
									}
								}}
								role="presentation"
							/>
						{/each}
					</div>
				{:else}
					<PageNote>
						<Icon icon="image-off" size="50" />
						No photo here
					</PageNote>
				{/if}
				
				<Note note={error.error} status="400" --note-margin-top="16px"></Note>

				{#if unused.length > 0}
					<div class="line btns">
						<Button
							onclick={() => {
								if (files.length != unused.length) {
									files = unused;
								} else {
									files = [];
								}
							}}
						>
							Select
							{#if files.length != unused.length}
								All
							{:else}
								None
							{/if}
						</Button>
						<Button
							--button-background-color-hover="red"
							--button-background-color="darkred"
							onclick={remove}
							disabled={files.length == 0}
						>
							Delete ({files.length})
						</Button>
					</div>
				{/if}
			</div>
		{/if}
	</div>

	<hr />

	<div class="fold">
		<div class="group_title">
			User{users.length > 1 ? 's' : ''} ({users.length}) with missing photo
			<FoldButton
				open={open_users}
				onclick={() => {
					open_users = !open_users;
				}}
			/>
		</div>

		{#if open_users}
			<div transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each users as x}
					<a href="/@{x.username}">{x.name}</a>

					<br />
				{:else}
					<PageNote>
						<Icon icon="x" size="50" />
						No user here
					</PageNote>
				{/each}
			</div>
		{/if}
	</div>

	<hr />

	<div class="fold">
		<div class="group_title">
			Post{posts.length > 1 ? 's' : ''} ({posts.length}) with missing photo / files
			<FoldButton
				open={open_posts}
				onclick={() => {
					open_posts = !open_posts;
				}}
			/>
		</div>

		{#if open_posts}
			<div transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each posts as x}
					<a href="/{x.slug}">{x.title}</a>

					<br />
				{:else}
					<PageNote>
						<Icon icon="x" size="50" />
						No post here
					</PageNote>
				{/each}
			</div>
		{/if}
	</div>
</Content>

<style>
	.fold {
		margin: var(--sp2) 0;
	}

	.group_title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;
	}

	.unused {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
	}

	img {
		width: 100px;
		border-radius: var(--sp0);
		cursor: pointer;
		background-color: var(--bg2);
	}
	img.selected {
		outline: 4px solid red;
		outline-offset: -4px;
	}

	.btns {
		margin-top: var(--sp2);
	}
</style>
