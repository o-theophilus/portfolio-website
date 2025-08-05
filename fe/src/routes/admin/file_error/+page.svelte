<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import { loading, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button_old/fold.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Back from '$lib/button_old/back.svelte';
	import Log from '$lib/log.svelte';

	export let data;
	let { unused } = data;
	let { users } = data;
	let { posts } = data;

	let open_unused = unused.length > 0;
	let open_users = users.length > 0;
	let open_posts = posts.length > 0;

	let files = [];
	let error = {};

	const remove = async () => {
		error = {};

		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/file/error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ files })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			unused = unused.filter((x) => !files.includes(x));
			$notify.add(`Photo${files.length > 1 ? 's' : ''} Deleted`);
			files = [];
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Manage Files" description="Here you will find missing or excess images" />

<Content>
	<div class="title">
		<Back />
		<strong class="ititle"> Photo Error </strong>
	</div>

	<div class="fold">
		<div class="group_title">
			Unused Photo{unused.length > 1 ? 's' : ''} / Fils{unused.length > 1 ? 's' : ''} ({unused.length})
			<ButtonFold
				open={open_unused}
				on:click={() => {
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
						alt="unused file"
						on:click={() => {
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
					no photo here
				{/each}
			</div>

			{#if error.error}
				<div class="error">
					{error.error}
				</div>
			{/if}

			{#if unused.length > 0}
				<br />
				<div class="line">
					<Button
						on:click={() => {
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
					<Button extra="hover_red" on:click={remove} disabled={files.length == 0}>
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
			<ButtonFold
				open={open_users}
				on:click={() => {
					open_users = !open_users;
				}}
			/>
		</div>

		{#if open_users}
			<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each users as x}
					<a href="/profile?user={x.key}">{x.name}</a>

					<br />
				{:else}
					no user here
				{/each}
			</div>
		{/if}
	</div>

	<hr />

	<div class="fold">
		<div class="group_title">
			Post{posts.length > 1 ? 's' : ''} ({posts.length}) with missing photo / files
			<ButtonFold
				open={open_posts}
				on:click={() => {
					open_posts = !open_posts;
				}}
			/>
		</div>

		{#if open_posts}
			<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each posts as x}
					<a href="/{x.key}">{x.title}</a>

					<br />
				{:else}
					no post here
				{/each}
			</div>
		{/if}
	</div>
</Content>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

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
	}
</style>
