<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { page } from '$app/state';

	import { Datetime, Marked, Avatar } from '$lib/macro';
	import { Link, RoundButton, Like } from '$lib/button';
	import Add from './_add.svelte';
	import One from './one.svelte';
	import Delete from './one.delete.svelte';
	import Report from './one.report.svelte';

	let { post_key, update, search, comment, comments = [] } = $props();
	let error = $state({});
	let path = [...comment.path];
	path.push(comment.key);

	let open_menu = $state(false);
	let self = false;

	let _this;
	onMount(() => {
		if (`#${comment.key}` == page.url.hash) {
			_this.scrollIntoView({ behavior: 'smooth' });
		}
	});

	const submit_like = async (liked) => {
		error = {};

		let url = `${import.meta.env.VITE_BACKEND}/comment/like/${comment.key}`;
		if (Object.keys(search).length != 0) {
			url = `${url}?${new URLSearchParams(search).toString()}`;
		}

		let resp = await fetch(url, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ like: liked })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			comment = resp.comment;
		} else {
			error = resp;
		}
	};
</script>

<svelte:window
	onclick={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

<section bind:this={_this}>
	<div class="block">
		<Avatar name={comment.user.name} photo={comment.user.photo} />
		<div class="content">
			<div class="top">
				<div>
					<div class="name">{comment.user.name}</div>
					<div class="date"><Datetime datetime={comment.date} type="ago" /></div>
				</div>

				<div class="right">
					<RoundButton
						icon="ellipsis"
						onclick={() => {
							open_menu = !open_menu;
							self = true;
						}}
					/>

					{#if open_menu}
						<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
							{#if comment.user.key == app.user.key}
								<Link small onclick={() => module.open(Delete, { comment, update })}>Delete</Link>
							{:else}
								<Link
									small
									onclick={() => {
										module.open(Report, {
											reported: {
												key: comment.user.key,
												name: comment.user.name,
												photo: comment.user.photo
											},
											entity: {
												type: 'comment',
												key: comment.key,
												extra: comment.comment
											}
										});
									}}
								>
									Report
								</Link>
							{/if}
						</div>
					{/if}
				</div>
			</div>

			<div class="comment">
				<Marked content={comment.comment} />
			</div>

			{#if error.error}
				<div class="error" transition:slide>
					{error.error}
				</div>
			{/if}

			{#if app.user.login}
				<div class="line">
					<RoundButton
						icon="reply"
						onclick={() =>
							module.open(Add, { post_key, path, comment: comment.comment, update, search })}
					/>

					<Like
						--like-height="32px"
						like={comment.like.length}
						dislike={comment.dislike.length}
						onlike={() => {
							comment.dislike = comment.dislike.filter((e) => e != app.user.key);
							if (comment.like.includes(app.user.key)) {
								comment.like = comment.like.filter((e) => e != app.user.key);
							} else {
								comment.like.push(app.user.key);
							}
							submit_like(true);
						}}
						ondislike={() => {
							comment.like = comment.like.filter((e) => e != app.user.key);
							if (comment.dislike.includes(app.user.key)) {
								comment.dislike = comment.dislike.filter((e) => e != app.user.key);
							} else {
								comment.dislike.push(app.user.key);
							}
							submit_like(false);
						}}
					/>
				</div>
			{/if}
		</div>
	</div>

	{#each comments as x}
		{#if x.path[x.path.length - 1] == comment.key}
			<One comment={x} {comments} {post_key} {update} {search} />
		{/if}
	{/each}
</section>

<style>
	section {
		padding: var(--sp2);
		padding-right: 0;
		/* padding-bottom: 0; */

		border: 2px solid var(--bg2);
		border-right-width: 0;
		/* border-bottom-width: 0; */

		margin-top: var(--sp2);

		border-top-left-radius: var(--sp0);
	}

	.block {
		display: flex;
		gap: var(--sp2);
	}
	.content {
		width: 100%;
	}
	.top {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.top {
		justify-content: space-between;
	}

	.date {
		font-size: 0.8rem;
		transition: color var(--trans);
	}
	.comment,
	.name {
		color: var(--ft1);
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
		margin-top: var(--sp2);
		/* margin-bottom: var(--sp2); */
	}

	.right {
		position: relative;
	}
	.menu {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		width: max-content;
		position: absolute;
		top: 30px;
		right: 0;
		padding: var(--sp2);
		background-color: var(--bg2);
		border-radius: var(--sp1);
	}

	.error {
		color: red;
		font-size: 0.8rem;
		margin-top: 16px;
	}
</style>
