<script>
	import { Button, FoldButton } from '$lib/button';
	import { Avatar, Datetime } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Form from './_form.svelte';

	let { block, update } = $props();
	let open = $state(false);
</script>

<div class="one">
	<div class="user">
		<a href="/@{block.user.username}">
			<Avatar name={block.user.name} photo={block.user.photo} --avatar-border-radius="50%" />
		</a>
		<div class="right">
			<a href="/@{block.user.username}" class="name">
				{block.user.name}
			</a>

			<div class="username">
				@{block.user.username}
			</div>
		</div>
		<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
	</div>

	{#if open}
		<div class="report" transition:slide>
			<a href="/@{block.admin.username}">
				<Avatar name={block.admin.name} photo={block.admin.photo} --avatar-border-radius="50%" />
			</a>
			<div class="right">
				<a href="/@{block.admin.username}" class="name">
					{block.admin.name}
				</a>

				<div class="username">
					@{block.admin.username}
				</div>

				<div class="comment_area">
					<div class="date">
						<Datetime datetime={block.date_created} type="date_numeric"></Datetime>
						<Datetime datetime={block.date_created} type="time_12h"></Datetime>
					</div>
					<div class="comment">
						{block.comment}
					</div>
				</div>

				{#if app.user.access.includes('block:unblock')}
					<Button
						icon="lock-open"
						--button-font-size="0.8rem"
						--button-height="32px"
						onclick={() => module.open(Form, { key: block.user.key, update })}
					>
						Unblock
					</Button>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.one {
		background-color: var(--bg1);

		border-radius: 8px;
		margin: 8px 0;
	}

	.user {
		display: flex;
		gap: 16px;
		padding: 16px;
		align-items: center;
	}
	.right {
		width: 100%;
	}

	.report {
		display: flex;
		gap: 16px;

		padding: 16px;
		border-top: 2px solid var(--bg2);
	}

	.comment_area {
		margin: 16px 0;
	}
	.name {
		font-weight: 700;
		color: var(--ft1);
	}
	.username {
		font-size: 0.7em;
	}

	.date {
		font-size: 0.7rem;
	}

	a {
		color: var(--ft2);
		text-decoration: none;
	}
</style>
