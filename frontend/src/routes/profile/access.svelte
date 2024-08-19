<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Tag from '$lib/button/tag.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Access_Ok from './access._ok.svelte';
	import Icon from '$lib/icon.svelte';

	export let user;
	export let access;
	let mods = [...user.access];
	let init = [...user.access];
	let open = false;

	const select_group = (_in) => {
		let group = [];
		for (const [name, r0les] of Object.entries(access)) {
			for (const x of r0les) {
				if (_in == name) {
					group.push(`${name}:${x[0]}`);
				} else if (_in == x[1]) {
					group.push(`${name}:${x[0]}`);
				} else if (!_in) {
					group.push(`${name}:${x[0]}`);
				}
			}
		}

		let add_all = false;
		for (const x of group) {
			if (!mods.includes(x)) {
				add_all = true;
				break;
			}
		}

		if (add_all) {
			for (const x of group) {
				if (!mods.includes(x)) {
					mods.push(x);
				}
			}
			mods = mods;
		} else {
			mods = mods.filter((x) => !group.includes(x));
		}
	};

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

<!-- TODO: redesign component with toggle-->

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
		<div class="grid">
			<span>
				<Link
					on:click={() => {
						select_group();
					}}
				>
					category
				</Link>
			</span>

			{#each [1, 2, 3] as x}
				<span>
					<Link
						on:click={() => {
							select_group(x);
						}}
					>
						Level {x}
					</Link>
				</span>
			{/each}

			{#each Object.entries(access) as [_type, _actions]}
				<span>
					<Link
						on:click={() => {
							select_group(_type);
						}}
					>
						{_type}
					</Link>
				</span>

				{#each [1, 2, 3] as x}
					<span>
						{#each _actions as action}
							{#if action[1] == x}
								<Tag
									active={mods.includes(`${_type}:${action[0]}`)}
									on:click={() => {
										select(`${_type}:${action[0]}`);
									}}
								>
									{action[0].split('_').join(' ')}
								</Tag>
							{/if}
						{/each}
					</span>
				{/each}
			{/each}
		</div>

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
		font-weight: 900;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: var(--sp2) 0;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(4, auto);
	}

	span {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp0);
		align-items: center;

		outline: 1px solid var(--bg2);
		padding: var(--sp0);
	}
</style>
