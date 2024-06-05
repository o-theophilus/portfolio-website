<script>
	import { module, user, portal, timeAgo } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	import Marked from '$lib/marked.svelte';
	import Button from '$lib/button/button.svelte';
	import Add_Comment from './comment__add__.svelte';
	import Comment from './comment.item.svelte';
	import Menu from './comment.item__menu__.svelte';

	export let comment = {};
	export let comments = [];
	let error = {};

	const validate = async (vote) => {
		error = {};

		if (comment.upvote.includes($user.key)) {
			comment.upvote = comment.upvote.filter((e) => e != $user.key);
		} else if (comment.downvote.includes($user.key)) {
			comment.downvote = comment.downvote.filter((e) => e != $user.key);
		}

		if (vote == 'up') {
			comment.upvote.push($user.key);
		} else if (vote == 'down') {
			comment.downvote.push($user.key);
		} else {
			return;
		}
		comment = comment;

		submit(vote);
	};

	const submit = async (vote) => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/vote/${comment.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ vote })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = {
				for: 'comment',
				data: resp.comments
			};
		} else {
			error = resp;
		}
	};

	let saturation = Math.floor(Math.random() * (360 + 1));

	let time = timeAgo(comment.created_at);
	onMount(() => {
		const intervalId = setInterval(() => {
			time = timeAgo(comment.created_at);
		}, 1000);

		return () => clearInterval(intervalId);
	});
</script>

<section>
	<div class="block">
		<div
			class="img"
			class:light={saturation > 29 && saturation < 189}
			style:--saturation={saturation}
		>
			{comment.user_name[0]}
		</div>
		<div class="content">
			<div class="top">
				<strong class="name">{comment.user_name}</strong>
				<div class="date_menu">
					<div class="date">{time}</div>
					<div
						class="menu"
						on:click={() => {
							$module = {
								module: Menu,
								comment
							};
						}}
						on:keypress
						role="presentation"
					>
						&#8226;&#8226;&#8226;
					</div>
				</div>
			</div>

			<div class="comment">
				<Marked md={comment.comment} />
			</div>
			{#if error.error}
				<span class="error">
					{error.error}
				</span>
				<br />
			{/if}
			{#if $user.login}
				<div class="buttons">
					<Button
						icon="quote"
						class="secondary tiny"
						on:click={() => {
							$module = {
								module: Add_Comment,
								owner_key: comment.key
							};
						}}
					/>
					|
					<Button
						name={comment.downvote.length}
						class="secondary tiny"
						icon="dislike"
						on:click={() => {
							validate('down');
						}}
					/>
					|
					<Button
						name={comment.upvote.length}
						class="secondary tiny"
						icon="like"
						on:click={() => {
							validate('up');
						}}
					/>
				</div>
			{/if}
		</div>
	</div>

	{#each comments as c}
		{#if c.path[c.path.length - 1] == comment.key}
			<Comment comment={c} {comments} />
		{/if}
	{/each}
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		padding: var(--sp2);
		padding-right: 0;
		padding-bottom: 0;

		border: 2px solid var(--ac4);
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
	.top,
	.date_menu {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.top {
		justify-content: space-between;
	}

	.img {
		--size: 40px;

		background-color: hsl(var(--saturation), 100%, 50%);
		border-radius: 50%;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		display: flex;
		align-items: center;
		justify-content: center;

		text-transform: capitalize;
		font-size: larger;
		font-weight: bold;

		color: var(--ac5_);
	}
	.light {
		color: var(--ac1_);
	}
	.date {
		color: var(--ac3);
	}
	.menu {
		cursor: pointer;
	}
	.menu:hover {
		color: var(--cl1);
	}
	.comment,
	.name {
		color: var(--ac1);
	}

	.buttons {
		display: flex;
		gap: var(--sp1);
		padding-bottom: var(--sp1);
	}
</style>
