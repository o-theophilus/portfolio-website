<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Link } from '$lib/button';
	import { Avatar, Spinner } from '$lib/macro';
	import Button from '../button.svelte';
	import Form from './edit.svelte';

	let { author, post, edit_mode, loading, update } = $props();
</script>

{#if loading || author.username}
	<hr />
	{#if app.user.access.includes('post.edit_author') && edit_mode}
		<Button onclick={() => module.open(Form, { key: post.key, update })}>Edit Author</Button>
	{/if}

	<div class="line">
		{#if loading}
			<Spinner active={loading} size="20" />
			<span class="small"> | </span>
			<span class="small"> Author </span>
		{:else}
			<Link href="/@{author.username}">
				<Avatar name={author.name} photo={author.photo} --avatar-border-radius="50%" />
			</Link>
			<div class="details">
				<div class="line">
					<Link href="/@{author.username}" --link-font-size="0.8rem">
						{author.name}
					</Link>
					<span class="small"> | </span>
					<span class="small"> Author </span>
				</div>
				<div class="username">
					@{author.username}
				</div>
			</div>
		{/if}
	</div>
{/if}

<style>
	.line {
		gap: 16px;
	}

	.small {
		font-size: 0.8rem;
	}
	.username {
		font-size: 0.7rem;
	}
</style>
