<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Button from '$lib/button/button.svelte';
	import Back from '$lib/button/back.svelte';
	import Log from '$lib/log.svelte';

	export let data;
	let { unused } = data;
	let { users } = data;
	let { posts } = data;

	let open_unused = unused.length > 0;
	let open_users = users.length > 0;
	let open_posts = posts.length > 0;

	let photos = [];
	let error = {};

	const remove = async () => {
		error = {};

		$loading = 'deleting . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo/error`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ photos })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			unused = unused.filter((x) => !photos.includes(x));
			$notification = {
				status: 200,
				message: `Photo${photos.length > 1 ? 's' : ''} Deleted`
			};
			photos = [];
		} else {
			error = resp;
		}
	};
</script>

<Log entity_type={'page'} />
<Meta title="Manage Photos" description="Here you will find missing or excess images" />

<Content>
	<div class="left">
		<Back />
		<strong class="ititle"> Photo Error </strong>
	</div>

	<div class="fold">
		<div class="title">
			Unused Photo{unused.length > 1 ? 's' : ''} ({unused.length})
			<ButtonFold
				open={open_unused}
				on:click={() => {
					open_unused = !open_unused;
				}}
			/>
		</div>

		{#if open_unused}
			<div class="unused" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each unused as x}
					<img
						class:selected={photos.includes(x)}
						src={`${x}/100` || ''}
						alt="missing"
						onerror="this.src='/site/no_photo.png'"
						on:click={() => {
							if (photos.includes(x)) {
								photos = photos.filter((y) => y != x);
							} else {
								photos.push(x);
								photos = photos;
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
				<div class="row">
					<Button
						on:click={() => {
							if (photos.length != unused.length) {
								// photos = [];
								photos = unused;
							} else {
								photos = [];
							}
						}}
					>
						Select
						{#if photos.length != unused.length}
							All
						{:else}
							None
						{/if}
					</Button>
					<Button extra="hover_red" on:click={remove} disabled={photos.length == 0}
						>Delete ({photos.length})</Button
					>
				</div>
			{/if}
		{/if}
	</div>

	<hr />

	<div class="fold">
		<div class="title">
			User{users.length > 1 ? 's' : ''} ({users.length})
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
		<div class="title">
			Post{posts.length > 1 ? 's' : ''} ({posts.length})
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
					<a href="/{x.key}">{x.name}</a>

					<br />
				{:else}
					no post here
				{/each}
			</div>
		{/if}
	</div>
</Content>

<style>
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.fold {
		margin: var(--sp2) 0;
	}
	.title {
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;
	}

	.row {
		display: flex;
		gap: var(--sp1);
	}

	.unused {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}
	img {
		border-radius: var(--sp0);
		cursor: pointer;
	}
	img.selected {
		outline: 2px solid var(--cl1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
