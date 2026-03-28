<script>
	import { Button, FoldButton } from '$lib/button';
	import { Datetime, User } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Dismiss from './one.dismiss.svelte';
	import Resolve from './one.resolve.svelte';

	let { report, update, searchParams } = $props();
	let open = $state(false);
</script>

<div class="one">
	<div class="reported_user">
		<div class="user_date">
			<User user={report.reported.user}></User>
			<div class="right">
				<Datetime datetime={report.reporter.date_created} type="ago" />
				<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
			</div>
		</div>
	</div>

	{#if report.reported.comment_key}
		<div class="reported_comment">
			<Datetime datetime={report.reported.date_created} type="ago" />

			<div class="comment">
				{report.reported.comment}
			</div>
		</div>
	{/if}

	{#if open}
		<div transition:slide>
			<div class="reporter">
				<User user={report.reporter.user}></User>
				<div class="comment">
					{report.reporter.comment}
					{#each report.reporter.tags as tag}
						#{tag}
					{/each}
				</div>
			</div>

			{#if report.status == 'active' && app.user.access.includes('report.resolve')}
				<div class="btns">
					<Button
						icon="check"
						--button-font-size="0.8rem"
						--button-height="32px"
						onclick={() => module.open(Resolve, { report, update, searchParams })}
					>
						Resolve
					</Button>
					<Button
						icon="check"
						--button-font-size="0.8rem"
						--button-height="32px"
						onclick={() => module.open(Dismiss, { report, update, searchParams })}
					>
						Dismiss
					</Button>
				</div>
			{:else if report.resolver}
				<div class="resolver">
					<div class="user_date">
						<User user={report.resolver.user}></User>
						<Datetime datetime={report.resolver.date_created} type="ago" />
					</div>
					<div class="comment">
						{report.resolver.comment}
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.one {
		background-color: var(--bg3);

		border-radius: 8px;
		margin-top: 8px;
	}

	.reported_user,
	.reported_comment {
		padding: 16px;
	}

	.right {
		display: flex;
		align-items: flex-start;
		gap: 16px;
	}

	.reporter,
	.resolver {
		padding: 16px;
		border-top: 1px solid var(--ol);
	}

	.user_date {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 16px;

		font-size: 0.7rem;
	}
	.comment {
		margin-top: 8px;
	}

	.btns {
		display: flex;
		gap: 8px;

		padding: 16px;
		border-top: 1px solid var(--ol);
	}
</style>
