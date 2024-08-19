<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Toggle from '$lib/toggle.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Access_Ok from './access._ok.svelte';
	import Icon from '$lib/icon.svelte';

	export let user;
	export let access;
	let mods = [...user.access];
	let init = [...user.access];
	let open = true;
	let sub_open = '';

	const select = (_in) => {
		if (mods.includes(_in)) {
			mods = mods.filter((x) => x != _in);
		} else {
			mods.push(_in);
			mods = mods;
		}
	};

	let disabled = true;
	$: {
		let t1 = mods.sort((a, b) => a - b).join(',');
		let t2 = init.sort((a, b) => a - b).join(',');
		disabled = t1 == t2;
	}
</script>

<div class="title">
	Access
	<ButtonFold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</div>

{#if open}
	<section transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#each Object.entries(access) as [_type, level]}
			<div
				class="type"
				role="presentation"
				on:click={() => {
					if (sub_open == _type) {
						sub_open = '';
					} else {
						sub_open = _type;
					}
				}}
			>
				{_type}
			</div>
			{#if sub_open == _type}
				<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
					{#each Object.entries(level) as [lv, actions]}
						<div class="sub_type">
							Level {lv}
						</div>

						{#each actions as ac}
							<div class="line">
								<span>
									{ac.split('_').join(' ')}
								</span>

								<Toggle
									active={mods.includes(`${_type}:${ac}`)}
									on:click={() => {
										select(`${_type}:${ac}`);
									}}
								/>
							</div>
						{/each}
					{/each}
				</div>
			{/if}
		{/each}

		<br />

		<Button
			{disabled}
			on:click={() => {
				$module = {
					module: Access_Ok,
					key: user.key,
					access: mods
				};
			}}
		>
			Submit
			<Icon icon="send" />
		</Button>
	</section>
{/if}

<style>
	section {
		margin: var(--sp2) 0;
	}
	.title {
		font-weight: 800;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;
	}

	.type {
		padding: var(--sp1) 0;
		cursor: pointer;
		text-transform: capitalize;
		font-weight: 900;

		border-bottom: 1px solid var(--bg2);
	}

	.sub_type {
		font-weight: 900;
		font-size: 0.8rem;
		margin: var(--sp1) 0;
	}

	.line {
		font-size: 0.8rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp2);
		margin: var(--sp0) 0;
	}
</style>
