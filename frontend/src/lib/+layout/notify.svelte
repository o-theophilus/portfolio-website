<script>
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import One from './notify.one.svelte';

	let notifications = [];

	const get_key = () => {
		const chars = '0123456789abcdef';
		let code = '#';

		for (let i = 0; i < 10; i++) {
			code += chars[Math.floor(Math.random() * chars.length)];
		}
		return code;
	};

	export const add = (message, status = 200) => {
		notifications.push({
			message,
			status,
			key: get_key()
		});
		notifications = notifications;
	};
</script>

<section>
	{#each notifications as one (one.key)}
		<div
			class="one"
			transition:fade={{ delay: 0, duration: 250, easing: cubicInOut }}
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
		>
			<One
				{one}
				on:close={() => {
					notifications = notifications.filter((x) => x.key != one.key);
				}}
			/>
		</div>
	{/each}
</section>

<style>
	section {
		position: fixed;
		top: var(--headerHeight);
		right: 0;

		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: var(--sp1);

		pointer-events: none;
	}
</style>
