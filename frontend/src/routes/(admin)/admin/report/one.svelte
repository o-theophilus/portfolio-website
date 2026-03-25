<script>
	import { Button, FoldButton } from '$lib/button';
	import { app, module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Comment from '../../../(app)/[slug]/comment/one.svelte';
	import Dismiss from './one.dismiss.svelte';
	import Resolve from './one.resolve.svelte';

	let { report, update, searchParams } = $props();

	let open = $state(false);
</script>

<div class="one">
	<div class="reported">
		{#if report.reported_user}
			<Comment comment={report.reported_user}></Comment>
		{:else if report.reported_comment}
			<Comment comment={report.reported_comment}></Comment>
		{/if}

		<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
	</div>

	{#if open}
		<div transition:slide>
			<div class="reporter">
				<Comment comment={report.reporter}></Comment>
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
					<Comment comment={report.resolver}></Comment>
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

	.reported {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 16px;

		padding: 16px;
	}

	.reporter {
		padding: 16px;
		border-top: 1px solid var(--ol);
	}

	.btns {
		display: flex;
		gap: 8px;

		padding: 16px;
		border-top: 1px solid var(--ol);
	}

	.resolver {
		padding: 16px;
		border-top: 1px solid var(--ol);
	}
</style>
