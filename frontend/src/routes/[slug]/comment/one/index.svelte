<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, user } from '$lib/store.js';

	import Datetime from '$lib/datetime.svelte';
	import Link from '$lib/button/link.svelte';
	import BRound from '$lib/button/round.svelte';
	import Add from '../_add.svelte';
	import Comment from './index.svelte';
	import Marked from '$lib/marked.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';
	import Like from './like.svelte';

	export let post_key;
	export let update;
	export let comment = {};
	export let comments = [];
	let error = {};
	let path = [...comment.path];
	path.push(comment.key);

	let open_menu = false;
	let self = false;
</script>

<svelte:window
	on:click={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

<section id={comment.key}>
	<div class="block">
		<Avatar name={comment.user.name} photo={comment.user.photo} />
		<div class="content">
			<div class="top">
				<div>
					<strong class="name">{comment.user.name}</strong>
					<div class="date"><Datetime datetime={comment.date} type="ago" /></div>
				</div>

				<div class="right">
					<BRound
						icon="more_horiz"
						on:click={() => {
							open_menu = !open_menu;
							self = true;
						}}
					/>

					{#if open_menu}
						<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
							{#if comment.user.key == $user.key}
								<Link
									on:click={() => {
										$module = {
											module: Delete,
											comment,
											update
										};
									}}
								>
									Delete
								</Link>
							{/if}
							<Link
								on:click={() => {
									$module = {
										module: Report,
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
									};
								}}
							>
								Report
							</Link>
						</div>
					{/if}
				</div>
			</div>

			<div class="comment">
				<Marked content={comment.comment} />
			</div>

			{#if error.error}
				<div class="error">
					{error.error}
				</div>
			{/if}

			{#if $user.login}
				<div class="line">
					<BRound
						icon="reply"
						on:click={() => {
							$module = {
								module: Add,
								post_key,
								path,
								comment: comment.comment,
								update
							};
						}}
					/>

					<Like
						{comment}
						{update}
						on:update={(e) => {
							comment = e.detail;
						}}
					/>
				</div>
			{/if}
		</div>
	</div>

	{#each comments as c}
		{#if c.path[c.path.length - 1] == comment.key}
			<Comment comment={c} {comments} {post_key} />
		{/if}
	{/each}
</section>

<style>
	section {
		padding: var(--sp2);
		padding-right: 0;
		padding-bottom: 0;

		border: 2px solid var(--bg2);
		border-right-width: 0;
		border-bottom-width: 0;

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
		font-size: small;
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
		padding-bottom: var(--sp1);
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
		margin: var(--sp2) 0;
	}
</style>
