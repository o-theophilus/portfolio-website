<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import { loading, notify, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { FoldButton, Button, BackButton } from '$lib/button';
	import { Meta, Log } from '$lib/macro';

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
		console.log(resp);
		
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
			Unused Photo{unused.length > 1 ? 's' : ''} / Fils{unused.length > 1 ? 's' : ''} ({unused.length})
			<FoldButton
				open={open_unused}
				onclick={() => {
					open_unused = !open_unused;
				}}
			/>
		</div>

		{#if open_unused}
			<div class="unused" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
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
				{:else}
					<div class="none">no photo here</div>
				{/each}
			</div>

			{#if error.error}
				<div class="error" transition:slide>
					{error.error}
				</div>
			{/if}

			{#if unused.length > 0}
				<br />
				<div class="line">
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
					<Button extra="hover_red" onclick={remove} disabled={files.length == 0}>
						Delete ({files.length})
					</Button>
				</div>
			{/if}
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
			<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each users as x}
					<a href="/@{x.username}">{x.name}</a>

					<br />
				{:else}
					<div class="none">no user here</div>
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
			<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each posts as x}
					<a href="/{x.slug}">{x.title}</a>

					<br />
				{:else}
					<div class="none">no post here</div>
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
		gap: var(--sp1);
	}

	img {
		width: 100px;
		border-radius: var(--sp0);
		cursor: pointer;
		background-color: var(--bg2);
	}
	img.selected {
		outline: 2px solid var(--cl1);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
		color: red;
		font-size: 0.8rem;
	}

	.none {
		font-size: 0.8rem;
	}
</style>
