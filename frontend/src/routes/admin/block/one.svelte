<script>
	import { Button } from '$lib/button';
	import { Card } from '$lib/layout';
	import { Avatar, Datetime } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Form from './one.form.svelte';

	let { block, update, searchParams } = $props();
	let open = $state(false);
</script>

<Card
	{open}
	onclick={() => (open = !open)}
	--card-content-top-border-color="var(--ol)"
	--card-title-padding="16px"
	--card-content-padding="16px"
	--card-background-color="var(--bg3)"
	--card-outline-color="var(--ol)"
>
	{#snippet title()}
		<div class="user">
			<a href="/@{block.user.username}">
				<Avatar name={block.user.name} photo={block.user.photo} --avatar-border-radius="50%" />
			</a>
			<div class="name_username">
				<a href="/@{block.user.username}" class="name">
					{block.user.name}
				</a>
				<br />
				<span class="username">
					@{block.user.username}
				</span>
			</div>
		</div>
	{/snippet}

	<div class="report">
		<a href="/@{block.admin.username}">
			<Avatar name={block.admin.name} photo={block.admin.photo} --avatar-border-radius="50%" />
		</a>
		<div class="right">
			<div class="line1">
				<div class="name_username">
					<a href="/@{block.admin.username}" class="name">
						{block.admin.name}
					</a>
					<br />
					<span class="username">
						@{block.admin.username}
					</span>
				</div>
				<span class="date">
					<Datetime datetime={block.date_created} type="ago"></Datetime>
				</span>
			</div>

			<div class="comment">
				{block.comment}
			</div>

			{#if app.user.access.includes('block:unblock')}
				<Button
					icon="lock-open"
					--button-font-size="0.8rem"
					--button-height="32px"
					--button-outline-color-hover="var(--ol)"
					onclick={() => module.open(Form, { user: block.user, update, searchParams })}
				>
					Unblock
				</Button>
			{/if}
		</div>
	</div>
</Card>

<style>
	.user {
		display: flex;
		gap: 16px;
		align-items: center;
	}

	.right {
		width: 100%;
	}

	.line1 {
		display: flex;
		justify-content: space-between;
		gap: 8px;
		flex-wrap: wrap;
	}

	.name_username {
		line-height: 100%;

		& .name {
			font-weight: 700;
			color: var(--ft1);
			font-size: 0.8em;
		}

		& .username {
			font-size: 0.7em;
		}
	}

	.report {
		display: flex;
		gap: 16px;

		& .comment {
			margin: 12px 0;
		}
		& .date {
			font-size: 0.7rem;
			flex-shrink: 0;
		}
	}

	a {
		color: var(--ft2);
		text-decoration: none;
		pointer-events: all;
	}
</style>
