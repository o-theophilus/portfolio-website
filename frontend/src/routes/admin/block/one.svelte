<script>
	import { module } from '$lib/store.svelte.js';
	import { Avatar } from '$lib/macro';
	import { Datetime } from '$lib/macro';
	import { FoldButton, Button } from '$lib/button';
	import { slide } from 'svelte/transition';
	import Unblock from './_unblock.svelte';

	let { one, update } = $props();
	let open = $state(false);
</script>

<div class="one">
	<div class="user">
		<a href="/@{one.user.username}">
			<Avatar name={one.user.name} photo={one.user.photo} --avatar-border-radius="50%" />
		</a>
		<div class="right">
			<a href="/@{one.user.username}" class="name">
				{one.user.name}
			</a>

			<div class="email">
				{one.user.email}
			</div>
		</div>
		<FoldButton {open} onclick={() => (open = !open)}></FoldButton>
	</div>

	{#if open}
		<div class="report" transition:slide>
			<a href="/@{one.admin.username}">
				<Avatar name={one.admin.name} photo={one.admin.photo} --avatar-border-radius="50%" />
			</a>
			<div class="right">
				<a href="/@{one.admin.username}" class="name">
					{one.admin.name}
				</a>

				<div class="email">
					{one.admin.email}
				</div>

				<div class="comment_area">
					<div class="date">
						<Datetime datetime={one.date_created} type="date_numeric"></Datetime>
						<Datetime datetime={one.date_created} type="time_12h"></Datetime>
					</div>
					<div class="comment">
						{one.comment}
					</div>
				</div>

				<Button
					icon="lock-open"
					--button-font-size="0.8rem"
					--button-height="32px"
					onclick={() => module.open(Unblock, { key: one.user.key, update })}>Unblock</Button
				>
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
	.email {
		font-size: 0.8em;
		word-wrap: break-word;
		word-break: break-all;
	}

	.date {
		font-size: 0.7rem;
	}

	a {
		color: var(--ft2);
		text-decoration: none;
	}
</style>
