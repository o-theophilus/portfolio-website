<script>
	import { app, module } from '$lib/store.svelte.js';
	import { Avatar } from '$lib/macro';
	import { Datetime } from '$lib/macro';
	import { FoldButton, Button } from '$lib/button';
	import { slide } from 'svelte/transition';
	import Form from './_form.svelte';

	let { item, update } = $props();
	let open = $state(false);
</script>

<div class="one">
	<div class="user">
		<a href="/@{item.user.username}">
			<Avatar name={item.user.name} photo={item.user.photo} --avatar-border-radius="50%" />
		</a>
		<div class="right">
			<a href="/@{item.user.username}" class="name">
				{item.user.name}
			</a>

			<div class="username">
				@{item.user.username}
			</div>
		</div>
		<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
	</div>

	{#if open}
		<div class="report" transition:slide>
			<a href="/@{item.admin.username}">
				<Avatar name={item.admin.name} photo={item.admin.photo} --avatar-border-radius="50%" />
			</a>
			<div class="right">
				<a href="/@{item.admin.username}" class="name">
					{item.admin.name}
				</a>

				<div class="username">
					@{item.admin.username}
				</div>

				<div class="comment_area">
					<div class="date">
						<Datetime datetime={item.date_created} type="date_numeric"></Datetime>
						<Datetime datetime={item.date_created} type="time_12h"></Datetime>
					</div>
					<div class="comment">
						{item.comment}
					</div>
				</div>

				{#if app.user.access.includes('block:unblock')}
					<Button
						icon="lock-open"
						--button-font-size="0.8rem"
						--button-height="32px"
						onclick={() => module.open(Form, { key: item.user.key, update })}
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
		padding: var(--sp2);
		align-items: center;
	}
	.right {
		width: 100%;
	}

	.report {
		display: flex;
		gap: 16px;

		padding: var(--sp2);
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
