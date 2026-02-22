<script>
	import { page } from '$app/state';
	import { Avatar, Datetime } from '$lib/macro';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Control from './one.control.svelte';
	import One from './one.svelte';

	let { comment, post, search, update } = $props();
	console.log(comment);

	let _this;
	onMount(() => {
		if (page.url.hash == `#${comment.key}`) {
			_this.scrollIntoView({ behavior: 'smooth' });
		}
	});
</script>

<section bind:this={_this} class:parent={parent ? false : true}>
	<div class="avatar_name_date">
		<Avatar name={comment.user.name} photo={comment.user.photo} --avatar-border-radius="50%" />

		<div class="name_date">
			<div class="name_username">
				<div class="name">{comment.user.name}</div>
				<div class="username">@{comment.user.username}</div>
			</div>
			<div class="date"><Datetime datetime={comment.date_created} type="ago" /></div>
		</div>
	</div>

	<div class="comment">
		{comment.comment}
	</div>

	<Control {comment} {post} {search} {update}></Control>

	{#each comment.replies as reply (reply.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One comment={reply} {post} {search} {update}></One>
		</div>
	{/each}
</section>

<style>
	section {
		margin-top: 8px;
		padding: 16px;
		border-radius: 4px;

		background-color: var(--bg1);
	}
	.parent {
		margin: unset;
		margin-bottom: 16px;
		border: 2px solid var(--bg2);
	}

	.avatar_name_date {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.name_date {
		display: flex;
		align-items: flex-start;
		gap: 8px 16px;
		justify-content: space-between;
		flex-wrap: wrap;

		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
		line-height: 100%;
		margin-bottom: 4px;
	}

	.date {
		font-size: 0.7rem;
		line-height: 100%;
	}

	.username {
		font-size: 0.7rem;
	}

	.comment {
		font-size: 0.8rem;
		margin-top: 16px;
	}
</style>
