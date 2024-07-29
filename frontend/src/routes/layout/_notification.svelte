<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { notification } from '$lib/store.js';

	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';
	import BRound from '$lib/button/round.svelte';

	let timer_1, timer_2;
	const close = () => {
		$notification = '';
	};

	let zero = false;
	$: {
		$notification;

		zero = false;
		clearTimeout(timer_1);
		clearTimeout(timer_2);

		timer_1 = setTimeout(() => {
			zero = true;
		}, 0);
		timer_2 = setTimeout(close, 5000);
	}
</script>

{#if $notification}
	<section
		class:bad={$notification.status == 400}
		class:caution={$notification.status == 201}
		transition:fade={{ delay: 0, duration: 250, easing: cubicInOut }}
	>
		<div class="line">
			{#if $notification.status == 201}
				<Icon icon="error" />
			{:else if $notification.status == 400}
				<Icon icon="cancel" />
			{:else}
				<Icon icon="check_circle" />
			{/if}

			<Marked content={$notification?.message || 'no message'} />

			<BRound icon="close" extra="hover_red" on:click={close} />
		</div>

		<div class="progress" class:zero />
	</section>
{/if}

<style>
	section {
		position: fixed;
		top: var(--headerHeight);
		right: 0;

		width: fit-content;
		max-width: 300px;
		overflow: hidden;

		display: flex;
		flex-direction: column;
		align-items: end;

		background-color: var(--cl3);
		border-radius: var(--sp0);
		color: var(--ft1_b);
		font-size: 0.8rem;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		padding: 0 var(--sp2);
	}

	.progress {
		width: 100%;
		height: 2px;
		background-color: var(--ft1_b);
	}
	.zero {
		transition: width 5s linear;
		width: 0;
	}

	.bad {
		background-color: var(--cl2);
	}
	.caution {
		background-color: var(--cl4);
	}
</style>
